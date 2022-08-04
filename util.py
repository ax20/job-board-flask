def logger(e):
    with open('site.log', 'a') as f:
        f.write(str(e) + '\n')
        f.close()