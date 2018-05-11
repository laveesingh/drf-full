from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(
        required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(
        choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(
        choices='STYLE_CHOICES', default='friendly')

    def create(self, validated_data):
        '''Create and return a new Snippet instance, given the validated data'''
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        '''Update and return an existing Snippet instance,
        given the validated data'''
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance


# Following functions are for illustration purposes only

def working_with_serializers():
    from snippets.models import Snippet
    from snippets.serializers import SnippetSerializer
    from rest_framework.renderers import JSONRenderer
    from rest_framework.parsers import JSONParser

    code1 = '''foo = "bar"
    def display(var):
        print("var:", var)'''
    code2 = '''const foo = "bar"
    const display = var => console.log("var:", var)
    '''
    # create Snippet instances
    snippet1 = Snippet(code=code1)
    snippet2 = Snippet(code=code2)

    # save instances to the db
    snippet1.save()
    snippet2.save()

    # create serializer instance
    serializer = SnippetSerializer(snippet)
    serializer.data  # => in native types (not exactly but this will do)

    # render the data to json
    content = JSONRenderer().render(serializer.data)  # => bytes(string)

    # deserialization
    from django.utils.six import BytesIO

    stream = BytesIO(content)
    data = JSONParser().parse(stream)  # => absolute native types

    # restore native types to fully populated object instance
    serializer = SnippetSerializer(data=data)
    serializer.is_valid()  # => True
    serializer.validated_data # => almost native types
    serializer.save() # => save instance to db
