"""
Utitlity class for mail formatting.
"""

from src.utils.processpipeline import ProcessPipeline


def transform_mail(mail, filters):
    pipeline = ProcessPipeline(filters)
    message = mail['Betreff'] + '\n' + mail['Text']
    return pipeline.execute(message)
