export const parseXML = (rawXML) => {
  let xmlData = null
  const header = []
  const xmlDoc = new DOMParser().parseFromString(rawXML, 'text/xml')
  if (xmlDoc && xmlDoc.documentElement && xmlDoc.documentElement.children) {
    const xmlRows = xmlDoc.documentElement.children
    let rowTag = null
    let rowChildLength = -1
    let initHeader = true
    xmlData = Array.from(xmlRows).map((row) => {
      if (!rowTag) {
        rowTag = row.tagName
      } else if (rowTag !== row.tagName) {
        console.err(`invalid tag found <${row.tagName}> expected <${rowTag}>`)
      }
      if (rowChildLength === -1) {
        rowChildLength = row.children.length
      } else if (rowChildLength !== row.children.length) {
        console.err(
          `invalid row length found <${row.children.length}> expected <${rowChildLength}>`
        )
      }
      const vals = Array.from(row.children).map((rowChild) => {
        if (initHeader) {
          header.push(rowChild.tagName)
        }
        return rowChild.innerHTML
      })
      initHeader = false
      return vals
    })
  }
  return [header, xmlData]
}
