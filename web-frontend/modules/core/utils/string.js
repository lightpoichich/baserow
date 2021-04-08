export const uuid = function () {
  let dt = new Date().getTime()
  const uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (dt + Math.random() * 16) % 16 | 0
    dt = Math.floor(dt / 16)
    return (c === 'x' ? r : (r & 0x3) | 0x8).toString(16)
  })
  return uuid
}

export const upperCaseFirst = function (string) {
  return string.charAt(0).toUpperCase() + string.slice(1)
}

/**
 * Source:
 * https://medium.com/@mhagemann/the-ultimate-way-to-slugify-a-url-string-in-javascript-b8e4a0d849e1
 */
export const slugify = (string) => {
  const a =
    'àáâäæãåāăąçćčđďèéêëēėęěğǵḧîïíīįìłḿñńǹňôöòóœøōõőṕŕřßśšşșťțûüùúūǘůűųẃẍÿýžźż·/_,:;'
  const b =
    'aaaaaaaaaacccddeeeeeeeegghiiiiiilmnnnnoooooooooprrsssssttuuuuuuuuuwxyyzzz------'
  const p = new RegExp(a.split('').join('|'), 'g')

  return string
    .toString()
    .toLowerCase()
    .replace(/\s+/g, '-') // Replace spaces with -
    .replace(p, (c) => b.charAt(a.indexOf(c))) // Replace special characters
    .replace(/&/g, '-and-') // Replace & with 'and'
    .replace(/[^\w-]+/g, '') // Remove all non-word characters
    .replace(/--+/g, '-') // Replace multiple - with single -
    .replace(/^-+/, '') // Trim - from start of text
    .replace(/-+$/, '') // Trim - from end of text
}
/**
 * According to https://www.w3resource.com/javascript/form/ip-address-validation.php
 */
export const isValidIp = (str) => {
  const regex = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/
  return regex.test(str)
}

/**
 * Really only checks if any dot split is empty
 * and if last value is more than one char (no tld with one char)
 * Also, localhost is perfectly valid, like anything in /etc/hosts arbitrarily added
 */
export const isValidDomain = (str) => {
  const domainSplit = str.split('.')
  return (
    (domainSplit.length > 1 &&
      domainSplit.every((val) => {
        return val !== ''
      }) &&
      domainSplit[domainSplit.length - 1].length > 1) ||
    str === 'localhost'
  )
}

/**
 * https://developer.mozilla.org/en-US/docs/Web/API/URL Compatibility matrix
 */
export const isValidURL = (str) => {
  let url
  try {
    url = new URL(str)
  } catch (_) {
    return false
  }
  const protoMatch =
    url.protocol === 'http:' ||
    url.protocol === 'https:' ||
    url.protocol === 'ftp:'
  // This may sound stupid, but URL tries to autofix the url if it thinks it can
  // So we need to check one last time if they're the same before assuming its valid
  // for example https:/test.com works without that.
  const originMatch = str.startsWith(url.origin)
  // Now we need to make sure the domain is correct, because URL only tells us if the URI part if its correct
  // Dumb way is to just know if there is more than one non-empty dot split values
  // domain www. is not valid, but www.d may as well be
  // I think tradeoff here is to not validate TLD and gTLD because they're just too dynamic to keep up with.
  const validDomain = isValidDomain(url.hostname) || isValidIp(url.hostname)
  return protoMatch && originMatch && validDomain
}

export const isValidEmail = (str) => {
  const pattern = /[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/i
  return !!pattern.test(str)
}

// Regex duplicated from
// src/baserow/contrib/database/fields/field_types.py#PhoneNumberFieldType
// Docs reference what characters are valid in PhoneNumberFieldType.getDocsDescription
// Ensure they are kept in sync.
export const isSimplePhoneNumber = (str) => {
  const pattern = /^[0-9NnXx,+._*()#=;/ -]{1,100}$/
  return pattern.test(str)
}

export const isSecureURL = (str) => {
  return str.toLowerCase().substr(0, 5) === 'https'
}

export const escapeRegExp = (string) => {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}
