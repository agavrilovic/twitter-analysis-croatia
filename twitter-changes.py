class Api(object):
  def GetFriends(self, user=None, userid=None, cursor=-1, maxUsers=100):
    '''Fetch the sequence of twitter.User instances, one for each friend.

    Args:
      user: the username or id of the user whose friends you are fetching.  If
      not specified, defaults to the authenticated user. [optional]

    The twitter.Api instance must be authenticated.

    Returns:
      A sequence of twitter.User instances, one for each friend
    '''
    #if not user and not self._oauth_consumer:
    #  raise TwitterError("twitter.Api instance must be authenticated")
    friendsCache = []
    if user:
      url = '%s/statuses/friends/%s.json' % (self.base_url, user)
    else:
      url = '%s/statuses/friends.json' % self.base_url
    parameters = {}
    if userid:
      parameters['user_id'] = userid
    cnt = 0
    while (maxUsers == -1 or maxUsers > cnt):
      if len(friendsCache) == 0:
        parameters['cursor'] = cursor
        if cursor == 0:
          break
        json = self._FetchUrl(url, parameters=parameters)
        try:
          data = simplejson.loads(json)
        except Exception, e:
          print 'ERROR: %s b/c of: %s' % (e, json)
          break
        cursor = data['next_cursor']
        self._CheckForTwitterError(data)
        friendsCache = [User.NewFromJsonDict(x) for x in data['users']]
        if cnt == 0 and len(friendsCache) == 0:
          return
      (result, friendsCache) = (friendsCache[0], friendsCache[1:])
      cnt += 1
      yield result
      