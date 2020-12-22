from django.core.exceptions import ValidationError

def validate_file_extension(self,value):
        if value.file.content_type != 'application/pdf':
            raise ValidationError(u'File Type not supported')