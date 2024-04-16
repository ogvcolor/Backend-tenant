from ..login.models import AccessLevel, UserAccessLevel
from ..login.serializers import LoginSerializerAccessLevel, LoginSerializerUserAccessLevel

import pandas as pd

def getAccessLevel(email):
    try:
        user_access = UserAccessLevel.objects.filter(user_email = email)
        access = AccessLevel.objects.filter(user_email = email)
    except:
        print('usuário não encontrado no banco')
    
    user_access_json = LoginSerializerUserAccessLevel(user_access, many = False)
    access_json = LoginSerializerAccessLevel(access, many = False)

    df_user_access = pd.DataFrame(user_access_json)
    df_access = pd.DataFrame(access_json)

    df = pd.merge(df_user_access, df_access, how='inner', left_on='access_level_id', right_on='id')

    return df