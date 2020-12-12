
BASE_TEMPLATE = '''
<!DOCTYPE html>
<html>
    <head>
        <meta charset='UTF-8'>
        <title>Telegram Login</title>
    </head>
    <body>
        {{ content | safe }}
    </body>
</html>
'''

PHONE_FORM = '''
<form action='./' method='get'>
    Phone (international format): <input name='phone' type='text' placeholder='+40712345678'>
    <input type='submit'>
</form>
'''

CODE_FORM = '''
<form action='./' method='get'>
    Telegram code: <input name='code' type='text' placeholder='70707'>
    <input type='submit'>
</form>
'''