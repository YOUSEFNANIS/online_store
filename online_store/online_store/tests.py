import tempfile
from pathlib import Path

from django.test import SimpleTestCase, override_settings


class MediaCacheHeadersTests(SimpleTestCase):
    def test_development_media_has_a_long_cache_lifetime(self):
        with tempfile.TemporaryDirectory() as media_root:
            image = Path(media_root, 'images', 'example.jpg')
            image.parent.mkdir()
            image.write_bytes(b'example image')

            with override_settings(MEDIA_ROOT=media_root):
                response = self.client.get('/media/images/example.jpg')

            self.assertEqual(response.status_code, 200)
            directives = set(response['Cache-Control'].split(', '))
            self.assertEqual(
                directives,
                {'public', 'max-age=31536000', 'immutable'},
            )
