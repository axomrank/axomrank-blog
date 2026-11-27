"use strict";

const adreScoreForm = document.querySelector("#adre-score-calculator");
const adrePaper = adreScoreForm.elements.namedItem("paper");
const adreTwoMarkGroup = document.querySelector("#adre-two-mark-group");
const adreScoreResult = document.querySelector("#adre-score-result");
const adreOneCorrect = adreScoreForm.elements.namedItem("one-correct");
const adreOneWrong = adreScoreForm.elements.namedItem("one-wrong");
const adreTwoCorrect = adreScoreForm.elements.namedItem("two-correct");
const adreTwoWrong = adreScoreForm.elements.namedItem("two-wrong");

function updateAdrePaper() {
  const graduate = adrePaper.value === "graduate";
  adreOneCorrect.max = adreOneWrong.max = graduate ? 125 : 150;
  adreTwoMarkGroup.hidden = adreTwoMarkGroup.disabled = !graduate;
  adreScoreResult.value = "";
}

adrePaper.addEventListener("input", updateAdrePaper);
adreScoreForm.addEventListener("input", () => {
  adreScoreResult.value = "";
});
adreScoreForm.addEventListener("submit", (event) => {
  event.preventDefault();

  const graduate = adrePaper.value === "graduate";
  const oneCorrect = adreOneCorrect.valueAsNumber;
  const oneWrong = adreOneWrong.valueAsNumber;
  const twoCorrect = graduate ? adreTwoCorrect.valueAsNumber : 0;
  const twoWrong = graduate ? adreTwoWrong.valueAsNumber : 0;
  const oneLimit = Number(adreOneCorrect.max);
  const twoLimit = graduate ? Number(adreTwoCorrect.max) : 0;

  if (oneCorrect + oneWrong > oneLimit || twoCorrect + twoWrong > twoLimit) {
    adreScoreResult.value = "Your correct and wrong answers exceed the number of questions in a section.";
    return;
  }

  const score = oneCorrect - oneWrong / 4 + 2 * twoCorrect - twoWrong / 2;
  const blank = 150 - oneCorrect - oneWrong - twoCorrect - twoWrong;
  const total = graduate ? 175 : 150;
  adreScoreResult.value = `Estimated score: ${score} out of ${total}. Blank answers: ${blank}.`;
});

updateAdrePaper();
adreScoreForm.hidden = false;
