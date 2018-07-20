HELPER_SETTINGS = {
    'INSTALLED_APPS': [
        'djangocms_internalsearch',
        'djangocms_internalsearch.test_utils.app_1_with_search_cms_config',
        'djangocms_internalsearch.test_utils.app_2_with_search_cms_config',
        'haystack',
        'tests.core',
        'djangocms_text_ckeditor',
    ],

    'HAYSTACK_CONNECTIONS': {
        'default': {
            'ENGINE': 'haystack.backends.elasticsearch2_backend.Elasticsearch2SearchEngine',
            'URL': 'http://127.0.0.1:9200/',
            'INDEX_NAME': 'haystack',
        },
    }
}


def run():
    from djangocms_helper import runner
    runner.cms('djangocms_internalsearch',  extra_args=[])


if __name__ == '__main__':
    run()
