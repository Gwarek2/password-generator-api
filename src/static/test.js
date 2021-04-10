document.querySelector('#test-form').addEventListener('submit', (e) => {
  e.preventDefault()
  const form = e.target
  url = form[0].value
  const frame = document.querySelector('iframe')
  frame.src = url
})