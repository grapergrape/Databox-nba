import unittest
from nba_helper_tests import TestStatsFetcher
from databox_tests import TestDataboxFeed
from github_helper_tests import TestGitHubFetcher


if __name__ == '__main__':
    # runs StatsFetcher, DataboxFeed tests, GitHubFetcher tests
    unittest.main()