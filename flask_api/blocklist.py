"""
This file just contains the blocklist of the JWT tokens.
It will be imported by app and the logout resource so that tokens can be added to the blocklist when
the user logs out. If you are using cloud deployment, and your service is going to sleep,
you can use firestore/ redis to store the tokens instead of the local cache.
Also clean up functionality should be added to remove outdated tokens, so the cache will not overflow.
"""

BLOCKLIST = set()
