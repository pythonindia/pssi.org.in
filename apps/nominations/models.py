from django.db import models
from django.conf import settings
from common.models import BaseModel

GENDER_CHOICES = (
    ('M', 'MALE'),
    ('F', 'FEMALE'),
)

NOMINATION_NAME_CHOICE = (
    ('Board Member', 'Board Member'),
    ('Kenneth Gonsalves', 'Kenneth Gonsalves')
)


class NominationType(BaseModel):
    name = models.CharField(
        max_length=100, choices=NOMINATION_NAME_CHOICE, db_index=True)
    slug = models.CharField(max_length=10, unique=True)
    active = models.BooleanField(
        "Whether this  type should be available to public",
        default=True
    )

    def __str__(self):
        return ('%s- %s ' % (self.name, self.slug))


class Nomination(BaseModel):
    ntype = models.ForeignKey('NominationType')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    fullname = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, db_index=True)
    self_nomiation = models.BooleanField(
        "Self Nomination ", default=False)
    contact_number = models.CharField(max_length=10)
    postal_address = models.TextField(default="Your Full address")
    profession = models.CharField(
        max_length=300,  default="I work/study at ...")
    contribution_info = models.TextField(
        default=''' Explain in detail about the candidate contribution''')
    references = models.TextField(
        default='''The references themselves must be people who are known by
        either their work in the Python community''')
    reason_to_join_board = models.TextField(
        default="Reason to join PSSI board ", blank=True)

    def __str__(self):
        return "{user}: {ntype} [{fullname}]".format(
            user=self.user.username,
            ntype=self.ntype.name,
            fullname=self.fullname
        )
