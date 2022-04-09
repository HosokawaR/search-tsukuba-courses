Vue.component("lecture-item", {
  props: ["lec"],
  data() {
    return {};
  },
  template: `
    <div class="result-row">
      <div class="row-point"><span>{{ lec.similarities }}</span>pt</div>
      <div class="row-name"><a :href="genURL(lec.id)" target="blank">{{ lec.name }}</a></div>
      <div class="row-desc">{{ lec.note }}</div>
      <div class="row-id">{{ lec.id }}</div>
    </div>
  `,
  methods: {
    genURL(lecID) {
      return `https://kdb.tsukuba.ac.jp/syllabi/2020/${lecID}/jpn/0/`;
    },
  },
});

SORRY_IMG_URL = "/static/img/sorry.png";
HATENA_IMG_URL = "/static/img/hatena.png";

const app = new Vue({
  delimiters: ["[[", "]]"],
  el: "#app",
  data: {
    keywords: "",
    lecs: [],
    isErrShow: false,
    errMsg: "",
    errImg: "",
  },
  methods: {
    search() {
      let that = this;
      that.lecs.splice(-that.lecs.length);
      if (that.keywords === "") {
        return;
      }
      axios
        .post("/search", {
          keywords: this.keywords,
        })
        .then(function (res) {
          const stat = res.data.stat;
          if (stat === 0) {
            that.errMsg = "";
            for (const lec of res.data.data) {
              that.lecs.push({
                similarities: lec[0],
                name: lec[1],
                note: lec[2],
                id: lec[3],
              });
            }
          } else if (stat === 404) {
            that.errMsg = `「${that.keywords}」の意味をコンピュータは理解できませんでした。
                            違うキーワードで試してみて下さい。`;
            that.errImg = HATENA_IMG_URL;
          } else {
            that.errMsg = `「${that.keywords}」は正しく処理できませんでした。`;
            that.errImg = SORRY_IMG_URL;
          }
        })
        .catch(function (err) {
          that.errMsg = "サーバエラーが発生しました。";
          that.errImg = SORRY_IMG_URL;
        });
    },
  },
});
