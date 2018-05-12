from django.contrib.auth.models import User
from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class SnippetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Snippet
        fields = ('owner', 'id', 'title', 'code',
                  'linenos', 'language', 'style')


class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'snippets')


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
    serializer.validated_data  # => almost native types
    serializer.save()  # => save instance to db
