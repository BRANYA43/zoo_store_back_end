from base.mixins import UUIDMixin
from base.test_cases import ModelTestCase


class UUIDMixinTest(ModelTestCase):
    def test_uuid_is_primary_key(self):
        uuid = self.get_field(UUIDMixin, 'uuid')
        self.assertTrue(uuid.primary_key)

    def test_mixin_is_abstract_model(self):
        self.assertTrue(self.get_meta_attr(UUIDMixin, 'abstract'))
