#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Optional, Tuple


def check_brackets(text: str, brackets: Tuple[str, ...]) -> bool:
    """Even entries of `brackets` should be the opening brackets"""
    opening_brackets = brackets[::2]
    closing_brackets = brackets[1::2]
    stack = []

    # TODO tokenize the text,
    # or jump a few character when a multi character bracket is found
    for start in range(len(text)):
        for i, o_bracket in enumerate(opening_brackets):
            if text.startswith(o_bracket, start):
                stack.append(closing_brackets[i])
                break
        for c_bracket in closing_brackets:
            if text.startswith(c_bracket, start):
                if c_bracket != stack.pop():
                    return False
                break

    return stack == []


def remove_comments(
    full_text: str, comment_start: str, comment_end: str
) -> Optional[str]:
    while comment_start in full_text or comment_end in full_text:
        try:
            start = full_text.index(comment_start)
            end = full_text.index(comment_end, start)
        except ValueError:
            return None

        full_text = full_text[:start] + full_text[end + len(comment_end) :]
    return full_text


def get_tag_prefix(
    text: str, opening_tags: Tuple[str, ...], closing_tags: Tuple[str, ...]
) -> Tuple[Optional[str], Optional[str]]:
    for otag in opening_tags:
        if text.startswith(otag):
            return (otag, None)
    for ctag in closing_tags:
        if text.startswith(ctag):
            return (None, ctag)

    return (None, None)


def check_tags(
    full_text: str, tag_names: Tuple[str, ...], comment_tags: Tuple[str, str]
) -> bool:
    text = remove_comments(full_text, comment_tags[0], comment_tags[1])
    if text is None:
        return False

    brackets = []
    for tag in tag_names:
        brackets.extend((f"<{tag}>", f"</{tag}>"))

    return check_brackets(text, tuple(brackets))


if __name__ == "__main__":
    brackets = ("(", ")", "{", "}")
    yeet = "(yeet){yeet}"
    yeeet = "({yeet})"
    yeeeet = "({yeet)}"
    yeeeeet = "(yeet"
    print(check_brackets(yeet, brackets))
    print(check_brackets(yeeet, brackets))
    print(check_brackets(yeeeet, brackets))
    print(check_brackets(yeeeeet, brackets))
    print()

    spam = "Hello, /* OOGAH BOOGAH */world!"
    eggs = "Hello, /* OOGAH BOOGAH world!"
    parrot = "Hello, OOGAH BOOGAH*/ world!"
    print(remove_comments(spam, "/*", "*/"))
    print(remove_comments(eggs, "/*", "*/"))
    print(remove_comments(parrot, "/*", "*/"))
    print()

    otags = ("<head>", "<body>", "<h1>")
    ctags = ("</head>", "</body>", "</h1>")
    print(get_tag_prefix("<body><h1>Hello!</h1></body>", otags, ctags))
    print(get_tag_prefix("<h1>Hello!</h1></body>", otags, ctags))
    print(get_tag_prefix("Hello!</h1></body>", otags, ctags))
    print(get_tag_prefix("</h1></body>", otags, ctags))
    print(get_tag_prefix("</body>", otags, ctags))
    print()

    spam = (
        "<html>"
        "  <head>"
        "    <title>"
        "      <!-- Ici j'ai écrit qqch -->"
        "      Example"
        "    </title>"
        "  </head>"
        "  <body>"
        "    <h1>Hello, world</h1>"
        "    <!-- Les tags vides sont ignorés -->"
        "    <br>"
        "    <h1/>"
        "  </body>"
        "</html>"
    )
    eggs = (
        "<html>"
        "  <head>"
        "    <title>"
        "      <!-- Ici j'ai écrit qqch -->"
        "      Example"
        "    <!-- Il manque un end tag"
        "    </title>-->"
        "  </head>"
        "</html>"
    )
    parrot = (
        "<html>"
        "  <head>"
        "    <title>"
        "      Commentaire mal formé -->"
        "      Example"
        "    </title>"
        "  </head>"
        "</html>"
    )
    tags = ("html", "head", "title", "body", "h1")
    comment_tags = ("<!--", "-->")
    print(check_tags(spam, tags, comment_tags))
    print(check_tags(eggs, tags, comment_tags))
    print(check_tags(parrot, tags, comment_tags))
    print()
