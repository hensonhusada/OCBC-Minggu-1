from apps.models import Model


class Loan(Model):
    __table__ = 'loan'
    __primary_key__ = 'loanid'

# class PsychologyArticle(Model):
#     __table__ = 'psychologyarticle'

class PsychologyArticleDetail(Model):
    __table__ = 'psychologyarticle_detail'
    __primary_key__ = 'index'
    __timestamps__ = False