from elasticsearch import Elasticsearch
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.views import APIView, View

from .mixins import LoginRequiredMixin
from .renderers import CSVRenderer


class Elastic(LoginRequiredMixin, APIView, CSVRenderer):
    def get(self, request):
        es = Elasticsearch(
            host='192.168.5.68',
            port=9201,
            use_ssl=True,
            verify_certs=True,
            ca_certs='/run/secrets/ca.crt',
            client_cert='/run/secrets/certificate.crt',
            client_key='/run/secrets/certificate.key'

        )
        sudo = es.search(
            index="filebeat-*",
            body={"query": {
                    "bool": {
                        "must": [{
                            "term": {"system.auth.program": "sudo"}
                        }],
                        "must_not": [], "should": []
                    }
                },
                "from": 0, "size": 10, "sort": [], "aggs": {}
            }
        )
        return Response(sudo)


class index(LoginRequiredMixin, View):
    def get(self, request,):
        return render(
            request,
            'home.html',
        )
