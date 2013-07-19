#Copyright 2012 Newcastle University
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
from django.contrib import admin

from editor.models import Exam, Question, Extension, QuestionHighlight, EditorTag, TaggedQuestion

admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(QuestionHighlight)
admin.site.register(Extension)


class EditorTagAdmin(admin.ModelAdmin):
    list_display = ['name','official']
    actions = ['make_tag_official','merge_tags']

    def make_tag_official(self,request,queryset):
        queryset.update(official=True)
    make_tag_official.short_description = 'Make official'

    def merge_tags(self,request,queryset):
        if len(queryset)==1:
            return

        tags = list(queryset)
        tags.sort(key=EditorTag.used_count,reverse=True)
        merged_tag = tags[0]

        TaggedQuestion.objects.filter(tag__in=tags[1:]).update(tag=merged_tag)
        queryset.exclude(pk=merged_tag.pk).delete()

        self.message_user(request,"Tags %s merged into '%s'" % (', '.join("'%s'" % t.name for t in tags),merged_tag.name))
    merge_tags.short_description = 'Merge tags'

admin.site.register(EditorTag,EditorTagAdmin)
