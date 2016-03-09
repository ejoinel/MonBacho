# -*- coding: utf-8 -*-

from haystack import indexes
from MonBacho.models import Exam

class ExamIndex( indexes.SearchIndex, indexes.Indexable ):
    text = indexes.CharField( document=True, use_template=True )

    content_auto = indexes.EdgeNgramField( model_attr='name' )

    def get_model(self):
        return Exam

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
