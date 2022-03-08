# from django.core.exceptions import ObjectDoesNotExist

# from omens.models import Omen, PhilComment


# def import_comments(df):
#     ids = []
#     for i, row in df.dropna().iterrows():
#         try:
#             omen = Omen.objects.get(omen_num=row['omen'])
#         except ObjectDoesNotExist:
#             continue
#         com, _ = PhilComment.objects.get_or_create(
#             omen=omen
#         )
#         com.comment = row['commentary']
#         com.save()
#         ids.append(f"commentary {com} created")
#     return ids
