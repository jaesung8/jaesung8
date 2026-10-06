import unittest

from update_activity import EMPTY, END, START, render_activity, update_section


def event(kind="PullRequestEvent", repo="example/project", **payload):
    return {"type": kind, "public": True, "repo": {"name": repo},
            "created_at": "2026-10-06T02:00:00Z", "payload": payload}


class ActivityTests(unittest.TestCase):
    def test_untrusted_title_is_plain_text(self):
        value = event(action="opened", pull_request={"number": 4, "title": '<img src=x>\n[click](https://evil.test) `code`'})
        text, count = render_activity([value], "jaesung8")
        self.assertEqual(count, 1)
        self.assertNotIn("<img", text)
        self.assertNotIn("[click]", text)
        self.assertNotIn("\n", text)
        self.assertIn("https://github.com/example/project/pull/4", text)

    def test_preserve_outside_markers(self):
        source = "Before\r\n" + START + "\nold\n" + END + "\r\nAfter"
        self.assertEqual(update_section(source, "new"), "Before\r\n" + START + "\nnew\n" + END + "\r\nAfter")

    def test_invalid_markers(self):
        for source in ["missing", START, END + START, START + END + START, START + END + END]:
            with self.subTest(source=source), self.assertRaises(ValueError):
                update_section(source, "new")

    def test_generated_and_private_repositories_are_excluded(self):
        values = [event("PushEvent", "jaesung8/jaesung8"), event("PushEvent", "jaesung8/jaesung8.github.io")]
        private = event("PushEvent")
        private["public"] = False
        self.assertEqual(render_activity(values + [private], "jaesung8"), (EMPTY, 0))

    def test_empty_feed(self):
        self.assertEqual(render_activity([], "jaesung8"), (EMPTY, 0))

    def test_order_dedup_and_limit(self):
        values = [event(action="closed", pull_request={"number": 7, "merged": True}),
                  event(action="opened", pull_request={"number": 7})]
        values += [event(action="opened", pull_request={"number": number}) for number in range(6, 0, -1)]
        text, count = render_activity(values, "jaesung8")
        self.assertEqual(count, 5)
        self.assertIn("Merged PR", text.splitlines()[0])
        self.assertIn("#3", text.splitlines()[-1])
        self.assertEqual(text.count("/pull/7"), 1)

    def test_review_release_and_push(self):
        values = [event("PullRequestReviewEvent", action="submitted", pull_request={"number": 8},
                        review={"html_url": "https://evil.test/payload"}),
                  event("ReleaseEvent", action="published", release={"name": "v1", "html_url": "https://github.com/example/project/releases/tag/v1"}),
                  event("PushEvent", head="a" * 40)]
        text, count = render_activity(values, "jaesung8")
        self.assertEqual(count, 3)
        self.assertIn("Reviewed PR", text)
        self.assertIn("Published a release", text)
        self.assertIn("/commit/" + "a" * 40, text)
        self.assertNotIn("evil.test", text)


if __name__ == "__main__":
    unittest.main()
