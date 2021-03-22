export const parseXML = (rawXML) => {
  let xmlData = null
  const header = []
  const xmlDoc = new DOMParser().parseFromString(rawXML, 'text/xml')
  const parseErrors = xmlDoc.getElementsByTagName('parsererror')
  const errors = []
  if (parseErrors.length > 0) {
    Array.from(parseErrors).forEach((parseError) =>
      errors.push(parseError.textContent)
    )
  }
  if (xmlDoc && xmlDoc.documentElement && xmlDoc.documentElement.children) {
    const xmlRows = xmlDoc.documentElement.children
    xmlData = Array.from(xmlRows).map((row) => {
      const vals = Array.from(row.children).map((rowChild) => {
        const rowTag = rowChild.tagName
        if (!header.includes(rowTag)) {
          header.push(rowTag)
        }
        return { tag: rowTag, value: rowChild.innerHTML }
      })
      return vals
    })
  }
  xmlData = xmlData.map((line) => {
    return header.map((h) => {
      const lv = line.filter((lv) => lv.tag === h)
      return lv.length > 0 ? lv[0].value : ''
    })
  })
  return [header, xmlData, errors]
}
