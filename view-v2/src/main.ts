import axios from 'axios'

// const base = import.meta.env.BASE_URL

// axios.interceptors.request.use((config: any) => {
//   config.headers['cache-control'] = 'max-age=2147483647'; // always use cache, content never changes 
//   config.url = base + config.url
//   return config;
// });

// parse charIndex (behind #)
const initialCharIndex = parseInt(window.location.hash.slice(1)) || 900000

const contextFiles = 2

class Column {
  private textElements: {[fileIndex: number]: HTMLParagraphElement} = {}

  private estimatedColumnHeight = 0 // without padding
  private totalHeightUpdateDivisor = 1

  private scroll = document.createElement('div')

  private totalChars

  private paddingFactor = 0.66

  private currentCentralText = -1
  private cameFrom = -1

  private skipScroll = false
  public onScroll = (_charIndex: number) => {
    console.log('no on scroll handler set', _charIndex)
  }

  constructor(
    private name: string, 
    private map: number[], 
    private element: HTMLDivElement
  ) {
    this.scroll.className = 'scroll'
    this.element.appendChild(this.scroll)
    this.totalChars = map[map.length - 1]
    this.element.addEventListener('scroll', () => {
      this.handleScroll()
    }) 
  }

  async handleScroll() {
    if(this.skipScroll) {
      this.skipScroll = false
      return
    }
    let centralTextElement = this.textElements[this.currentCentralText]
    if(centralTextElement !== undefined) {

      const screenHeight = this.element.clientHeight
      const textHeight = centralTextElement.clientHeight
      const topPos = centralTextElement.offsetTop

      const scroll = this.element.scrollTop

      const middle = scroll + screenHeight / 2

      const progress = (middle - topPos) / textHeight

      let top = 0
      if(this.currentCentralText > 0) {
        top = this.map[this.currentCentralText - 1]
      }
      const bottom = this.map[this.currentCentralText]
      const charIndex = top + (bottom - top) * (1 - progress)
      if(charIndex < 0) {
        console.log('charIndex < 0', charIndex)
        console.log('top', top)
        console.log('bottom', bottom)
        console.log('progress', progress)
        console.log('middle', middle)
        console.log('topPos', topPos)
        console.log('textHeight', textHeight)
        console.log('screenHeight', screenHeight)
        console.log('scroll', scroll)
        console.log('currentCentralText', this.currentCentralText)
      }
      this.onScroll(charIndex)
      console.log('char index', charIndex)
      const newCharIndex = this.charToFile(charIndex)
      if(newCharIndex !== this.currentCentralText && newCharIndex !== this.cameFrom) {
        this.cameFrom = this.currentCentralText
        requestAnimationFrame(() => {
          this.setCharIndex(charIndex)
        }) 
      }
    }
  }

  async setCharIndex(charIndex: number) {
    let fi = this.charToFile(charIndex)

    const screenHeight = this.element.clientHeight
    const columnPadding = screenHeight * this.paddingFactor

    if(this.textElements[fi] == undefined) {
      let fiStr = fi.toString().padStart(5, '0')
      let textElement = document.createElement('p')
      textElement.className = 'text'
      this.textElements[fi] = textElement

      const text = await axios.get(`/volume/${this.name}/${fiStr}`, {responseType: 'text'})
      textElement.innerText = text.data
      this.scroll.appendChild(textElement)
    }
    let textElement = this.textElements[fi]

    let top = 0
    if(fi > 0) {
      top = this.map[fi - 1]
    }
    let bottom = this.map[fi]

    requestAnimationFrame(() => {
      const textHeight = textElement.clientHeight

      let columnHeight = textHeight * this.totalChars / (bottom - top)
      columnHeight = (columnHeight + this.estimatedColumnHeight * (this.totalHeightUpdateDivisor - 1)) / this.totalHeightUpdateDivisor
      this.estimatedColumnHeight = columnHeight
      this.totalHeightUpdateDivisor += 1
      this.scroll.style.height = columnHeight + columnPadding * 2 + 'px'

      const topPos = columnPadding + this.map[fi] / this.totalChars * columnHeight - textHeight
      textElement.style.top = `${topPos}px`

      const progress = (charIndex - top) / (bottom - top)
      const scroll = topPos + (1 - progress) * textHeight - 0.5 * screenHeight 
      this.skipScroll = true
      this.element.scrollTo(0, scroll)

      this.currentCentralText = fi
    })


    for(let i = 1; i <= contextFiles; i++) {
    }
  }

  charToFile(charIndex: number) {
    let fileLen = this.map.length
    let bottom = 0
    let top = fileLen
    let fi = Math.trunc(fileLen / 2)
    
    for(let i = 0; i < 100; i++) {
      if(fi == 0) {
        break
      } if(this.map[fi - 1] > charIndex) {
        top = fi
        fi = Math.trunc((bottom + fi) / 2)
      } else {
        if(this.map[fi] > charIndex) {
          break
        } else {
          bottom = fi
          fi = Math.trunc((fi + top) / 2)
        }
      }
    }
    return fi
  }
}

async function init() {
  // load levels
  let response = await axios.get('/volume/levels', {responseType: 'text'})
  const levels = parseInt(response.data)

  const endElement = document.getElementById('end')!

  const columns: Column[] = []
  for(let i = 0; i < levels + 1; i++) {
    let name = (levels - i).toString()
    if(i == levels) {
      name = 'original'
    }

    response = await axios.get(`/volume/maps/${name}.json`, {responseType: 'json'})
    const map = response.data
    const div = document.createElement('div')
    div.classList.add('text', 'column')
    endElement.insertAdjacentElement('beforebegin', div)

    const column = new Column(name, map, div)
    columns.push(column)
    column.setCharIndex(initialCharIndex)
  }

  // await creation of all columns
  requestAnimationFrame(() => {
    let animFrameRequest: number
    let lastCharIndex = initialCharIndex

    columns.forEach(column => {
      column.onScroll = (charIndex: number) => {
        if(animFrameRequest !== undefined) {
          cancelAnimationFrame(animFrameRequest)
        }
        animFrameRequest = requestAnimationFrame(() => {
          lastCharIndex = charIndex
          columns.forEach(otherColumn => {
            if(column !== otherColumn) {
              otherColumn.setCharIndex(charIndex)
            }
          })
        })
      }
    })

    window.addEventListener('resize', () => {
      if(animFrameRequest !== undefined) {
        cancelAnimationFrame(animFrameRequest)
      }
      animFrameRequest = requestAnimationFrame(() => {
        columns.forEach(column => {
          column.setCharIndex(lastCharIndex)
        })
      })
    })
  })
}

window.addEventListener('load', init)
