from elasticsearch_dsl.connections import connections
from django_elasticsearch_dsl import DocType, Index
from .models import Email_details
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search


client = Elasticsearch()
my_search = Search(using=client)


connections.create_connection()


email   = Index('application')

email.settings(
    number_of_shards=1,
    number_of_replicas=0
)

@email.doc_type
class Email_detailsDocument(DocType):

    class Meta:
        model = Email_details
        fields = ['email_id', 'subject', 'body', 'cc', 'bcc']



def search(subject):
    query = my_search.query("match", subject=subject)
    response = query.execute()
    return response