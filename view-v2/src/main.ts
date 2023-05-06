import axios from 'axios'

// const base = import.meta.env.BASE_URL

// axios.interceptors.request.use((config: any) => {
//   config.headers['cache-control'] = 'max-age=2147483647'; // always use cache, content never changes 
//   config.url = base + config.url
//   return config;
// });

// parse charIndex (behind #)
const initialCharIndex = parseInt(window.location.hash.slice(1)) || 0
console.log(initialCharIndex) 

class Column {
  constructor(
    private name: string, 
    private map: number[], 
    private element: HTMLDivElement
  ) {
  }

  async setCharIndex(charIndex: number) {
    let fi = this.charToFile(charIndex)
    console.log('file index:', fi)
    // pad fi with 5 zeros
    let fiStr = fi.toString().padStart(5, '0')
    const text = await axios.get(`/volume/${this.name}/${fiStr}`, {responseType: 'text'})
    this.element.innerText = text.data
  }

  charToFile(charIndex: number) {
    let fileLen = this.map.length
    let fi = Math.trunc(fileLen / 2)
    console.log('find', charIndex, 'in', this.map, 'fileLen', fileLen)
    
    for(let i = 0; i < 100; i++) {
      if(fi == 0) {
        break
      } if(this.map[fi - 1] > charIndex) {
        fi = Math.trunc(fi / 2)
      } else {
        if(this.map[fi] > charIndex) {
          break
        } else {
          fi = Math.trunc((fi + fileLen) / 2)
        }
      }
      console.log(fi)  
    }
    return fi
  }
}

async function init() {
  // load levels
  let response = await axios.get('/volume/levels', {responseType: 'text'})
  const levels = parseInt(response.data)

  console.log(levels)


  const endElement = document.getElementById('end')!

  for(let i = 0; i < levels + 1; i++) {
    let name = (levels - i).toString()
    console.log(i, levels)
    if(i == levels) {
      name = 'original'
    }
    response = await axios.get(`/volume/maps/${name}.json`, {responseType: 'json'})
    const map = response.data
    const div = document.createElement('div')
    div.classList.add('text', 'column')

    const column = new Column(name, map, div)

    column.setCharIndex(initialCharIndex)

    endElement.insertAdjacentElement('beforebegin', div)
  }
}

init()
