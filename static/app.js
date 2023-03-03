$form = $('#word');
$form.on('submit', getData);
$counter = $('#timer')
let score = 0;
let time = 60
$msg = $('#msg')
$score = $('#score')
$top_score = $('#top_score')
$n_played = $('#n_play')
const wordsList = new Set();


async function getData(e) {
    e.preventDefault()

    $inputVal = $('.word').val()
    const res = await axios.get('/valid-word', { params: { guess: $inputVal } });
    // console.log(res)

    if (res.data.result === 'not-on-board') {
        $msg.text("Word is not on board")
    }
    else if (res.data.result === 'not-word') {
        $msg.text("Error!!! Word does not exist")
    }
    else if (res.data.result === 'ok') {
        if (wordsList.has($inputVal)) {
            return $msg.text("Word already selected")
        }
        else {
            $msg.text("Valid Word")
            score += $inputVal.length
            wordsList.add($inputVal)
            console.log(wordsList)
        }
    }
    $score.text(`score: ${score}`)
    $('.word').val('')
}


let counting = setInterval(timer, 1000);
function timer() {
    time--
    $counter.text(time)
    if (time === 40) {
        clearInterval(counting)
        $('.word').hide()
        wordsList.clear()
        top_score()
    }
}

async function top_score() {
    const res = await axios.post('/score', { score: score })
    // console.log(res.data.n_played)
    $n_played.text(`Times Played: ${res.data.n_played}`)
    if (res.data.top_score) {
        $msg.hide()
        return $top_score.text(`New Top Score: ${score}`)
    }
    else {
        return $msg.text(`Final Score: ${score}`)
    }
}

