gotoprevious = document.getElementById('go-to-previous')
gotonext = document.getElementById('go-to-next')
gotonext.focus()


def keydown(event):
    if event.key == 'ArrowRight':
        gotonext.click()
    elif event.key == 'ArrowLeft':
        gotoprevious.click()


gotonext.onkeydown = keydown



