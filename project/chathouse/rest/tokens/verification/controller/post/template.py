from chathouse.utilities.security.validation.data.builder import TemplateBuilder
from chathouse.utilities.security.validation.data.field import Field

PostVerificationTemplateBuilder=TemplateBuilder()

PostVerificationTemplateBuilder.add(Field('email',regex='^(?=[\w_\-\.]+\@\w+\.\w+)[\w_\-\.@]{5,40}$',data_type=str)) #^(?=[\w_\-\.]+\@\w+\.\w+)[\w_\-\.@]{5,40}$
PostVerificationTemplateBuilder.add(Field('username',regex='^\w{6,30}$',data_type=str))
PostVerificationTemplateBuilder.add(Field('name',regex='[a-zA-Z]{3,25}',data_type=str))

IDSignUpVerificationTemplate=PostVerificationTemplateBuilder.template

PostVerificationTemplateBuilder.add(Field('identification',regex='^((?:\w{6,30})|(?:(?=[\w_\-\.]+\@\w+\.\w+)[\w_\-\.@]{5,40}))$',data_type=str))

IDLogInVerificationTemplate=PostVerificationTemplateBuilder.template


