# -*- coding: utf-8 -*-

#%%
import pytest

# import the script that contains the functions 
# instead of using  "/" use a "."
# allow you to access functions from other scripts
import create_dataframe_lecture as irc

#%%tests
# data
comment_row_1 = '01:17 < HeavenGuard> hello?\n' 
comment_row_2 = '19:29 <+Cogitabundus> Some like chaos.\n'
comment_row_3 = '19:29 <%Cogit1234> Some like chaos.\n'
comment_row_4 = '19:29 <~leeroy> Some like < User1234> \n'
join_quit_1 = '00:01 -!- Guest40341 [AndChat2541@AN-pl0gl1.8e2d.64f9.r226rd.IP] has quit [Quit: Bye]'
join_quit_2 = '18:39 -!- Hex [Hex@Quantum.Time] has quit [ < Hex> ]'
log_open_1 = '--- Log opened Tue Sep 20 00:01:49 2016'

# test is_message
@pytest.mark.parametrize('row,expected', [(comment_row_1, True), 
                                          (comment_row_2, True),
                                          (comment_row_3, True),
                                          (comment_row_4, True),
                                          (join_quit_1, False),
                                          (join_quit_2, False),
                                          (log_open_1, False)])
def test_is_message(row, expected):
    assert irc.is_message(row) == expected

@pytest.mark.parametrize('row, expected', [(comment_row_1, 'HeavenGuard'),
                                           (comment_row_2, 'Cogitabundus'),
                                           (comment_row_3, 'Cogit1234'),
                                           (comment_row_4, 'leeroy')])
def test_get_user_name(row, expected):
    assert irc.get_user_name(row) == expected
    
@pytest.mark.parametrize('row, expected', [(comment_row_1, 'hello?\n'),
                                           (comment_row_2, 'Some like chaos.\n'),
                                           (comment_row_3, 'Some like chaos.\n'),
                                           (comment_row_4, 'Some like < User1234> \n')])
def test_get_chat_message(row, expected):
    assert irc.get_chat_message(row) == expected



