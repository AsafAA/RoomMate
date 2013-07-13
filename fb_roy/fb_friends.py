import facebook as f

token = 'CAAHHJaqayWIBAH3lqJ6PbpLTwPHED34fxFQ3p2iZBnn6vf7ESjQ0Q7pGBZBld1nM2ZCh9ytdjndBbYe4dZCdGj6vM9tHPLK6PNkXAvxZBFnH9EQlDb6EpmmrTcEJqUq71VTie8PlaFHNEj2yzj0rl1WwgZCfd43fIZD'
def get_friends(token):
    graph = f.GraphAPI(token)
    friends = gr.get_connections('me','friends')
    return friends

