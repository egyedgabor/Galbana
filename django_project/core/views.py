from elasticsearch import Elasticsearch, exceptions as es_exceptions
from elasticsearch_dsl import Search, connections
from rest_framework.response import Response
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from rest_framework.views import APIView, View
import os

from .renderers import CSVRenderer
from .mixins import LoginRequiredMixin


def elastic():
    connections.configure(
        default={
            'hosts': os.environ['ELASTICSEARCH_HOST'],
            'port': os.environ['ELASTICSEARCH_PORT'],
            'use_ssl': True,
            'verify_certs': True,
            'ca_certs': '/run/secrets/ca.crt',
            'client_cert': '/run/secrets/certificate.crt',
            'client_key': '/run/secrets/certificate.key'

        },
    )

    es = Elasticsearch(
        host=os.environ['ELASTICSEARCH_HOST'],
        port=os.environ['ELASTICSEARCH_PORT'],
        use_ssl=True,
        verify_certs=True,
        ca_certs='/run/secrets/ca.crt',
        client_cert='/run/secrets/certificate.crt',
        client_key='/run/secrets/certificate.key'

    )
    try:
        es.info()
    except es_exceptions.ConnectionError:
        template = loader.get_template('not_working.html')
        context = {
            'host': os.environ['ELASTICSEARCH_HOST'],
            'port': os.environ['ELASTICSEARCH_PORT']
        }
        return ({
            'response': HttpResponse(template.render(context)),
            'status': 'ERROR'
        })
    return ({'response': es, 'status': 'OK'})


class Sudo(LoginRequiredMixin, APIView, CSVRenderer):
    def get(self, request):
        if elastic()['status'] == 'ERROR':
            return elastic()['response']
        else:
            es = elastic()['response']

        s = Search(using=es, index="filebeat-*").from_dict({
            "query": {
                "query_string": {
                  "query": "_exists_:system.auth.sudo",
                  "analyze_wildcard": 'true',
                }
            },

            "from": 0, "size": 1000,
            "sort": [
              "@timestamp"
            ], "aggs": {}
        }).execute().to_dict()

        return Response(s)


class Ssh(LoginRequiredMixin, APIView, CSVRenderer):
    def get(self, request):
        if elastic()['status'] == 'ERROR':
            return elastic()['response']
        else:
            es = elastic()['response']

        s = Search(using=es, index="filebeat-*").from_dict({
            "query": {
                "query_string": {
                  "query": "_exists_:system.auth.ssh.method",
                  "analyze_wildcard": 'true',
                }
            },
            "from": 0, "size": 1000,
            "sort": [
              "@timestamp"
            ], "aggs": {}
        }).execute().to_dict()

        return Response(s)


class Postgres(LoginRequiredMixin, APIView, CSVRenderer):
    def get(self, request):
        if elastic()['status'] == 'ERROR':
            return elastic()['response']
        else:
            es = elastic()['response']

        s = Search(using=es, index="filebeat-*").from_dict({
            "query": {
                "bool": {
                    "must": [{
                        "wildcard": {
                            "postgresql.log.user": "*"
                        }
                    }],
                    "must_not": [{
                        "term": {
                            "postgresql.log.user": "unknown"
                        }
                    }], "should": []
                }
            },

            "from": 0, "size": 1000, "sort": ['@timestamp'], "aggs": {}
        }).execute().to_dict()

        return Response(s)


class index(LoginRequiredMixin, View):
    def get(self, request,):
        return render(
            request,
            'home.html'
        )
