import requests as r
from models import Article, Comment

from .conversions import parseDate
from .users import assertUser
from pony.orm import db_session, commit, core
import logging

@db_session
def loadArticleAndSave(id: int):
    if not Article.exists(id=id):
        res = r.get("https://www.srf.ch/commentsapi/v1/public/srf/threads/urn:srf:article:{}".format(id)).json()
        if "statusCode" not in res.keys() and "welcomeMessage" in res.keys():
            logging.info("Discovered new article with open comment section. Title: {}".format(res["title"]))
            article = Article(id=id,commentsfetched=False,hascomments=True,created=parseDate(res["created"]),publicationdate=parseDate(res["publicationDate"]),kicker=res["kicker"],title=res["title"],welcomemessage=res["welcomeMessage"],frontendurl=res["frontendUrl"])
        elif "statusCode" in res.keys():
            if res["statusCode"] == 404:
                logging.info("Discovered new article without commenting possibility. Id: {}".format(id))
                article = Article(id=id,commentsfetched=True,hascomments=False)
        
        try:
            commit()
        except core.TransactionIntegrityError as e:
            if 'UNIQUE constraint failed' in str(e):
                pass
    

def loadAndSaveAllArticles(ids: list[int]):
    for id in ids:
        loadArticleAndSave(id)



def checkCommentsClosed(id: int):
    res = r.get("https://www.srf.ch/commentsapi/v1/public/srf/threads/urn:srf:article:{}".format(id)).json()
    if "statusCode" not in res.keys() and "welcomeMessage" in res.keys():
        return not (res["state"]=="open")
    

@db_session
def checkArticlesForNewlyClosed():
    articles = Article.select(lambda a: a.hascomments and not a.commentsfetched)
    for article in articles:
        if checkCommentsClosed(article.id):
            logging.info(f"Article with id {article.id} and title {article.title} has recently closed comments. Loading comments now...")
            getComments(article.id)
        

@db_session
def getComments(id: int):
    res = r.get("https://www.srf.ch/commentsapi/v1/public/srf/threads/urn:srf:article:{}/comments?nextToken=0&sort=created&limit=10000".format(id)).json()
    if res["hasMoreResults"] == "true":
        logging.ERROR("There have been more than 10'000 comments on an article. Cut at limit")
        # TODO implement this, unlikely
    
    if "entries" in res.keys():
        article = Article.get(id=id)
        for comment in res["entries"]:
            user = assertUser(comment["authorUsername"],comment["authorName"])
            if not Comment.exists(id=comment["id"]):
                commentObj = Comment(author=user,article=article,id=comment["id"],text=comment["text"],creationdate=parseDate(comment["creationDate"]),likes=comment["likes"])
                try:
                    commit()
                except core.TransactionIntegrityError as e:
                    if 'UNIQUE constraint failed' in str(e):
                        pass

                for reply in comment["replies"]:
                    replyUser = assertUser(reply["authorUsername"],reply["authorName"])
                    replyObj = Comment(author=replyUser,article=article,id=reply["id"],text=reply["text"],creationdate=parseDate(reply["creationDate"]),likes=reply["likes"],parentcomment=commentObj)

                    try:
                        commit()
                    except core.TransactionIntegrityError as e:
                        if 'UNIQUE constraint failed' in str(e):
                            pass

    article.commentsfetched = True
    commit()