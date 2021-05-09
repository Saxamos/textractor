#!/bin/bash

PROCESS="let x = ''
process.stdin.setEncoding('utf8')
process.stdin.on('data', chunk => x += chunk)
process.stdin.on('end', () => {
  try { x = eval(x) } catch(e) {}
  try { x = JSON.parse(x) } catch(e) {}
  const base = 'https://geco.amf-france.org/Bio/'
  const result = x
    .reduce((acc, d) => {
      if (!d.children[1] || !d.children[1].children[0].text) return acc
      const prev = acc.find(a => a.fund === d.children[1].children[0].text)
      if (prev) {
        prev.shares.push({
          isin: d.children[0].children[0].text,
          url: (base + d.children[0].children[0].href).replace(/&amp;/g, '&')
        })
        return acc
      }
      acc.push({
        shares: [{
          isin: d.children[0].children[0].text,
          url: (base + d.children[0].children[0].href).replace(/&amp;/g, '&')
        }],
        fund: d.children[1].children[0].text,
        prospectus: (base + d.children[2].children[0].href).replace(/&amp;/g, '&'),
      })
      return acc
    }, [])
  console.log(JSON.stringify(result, null, 2))
})"

# shellcheck disable=SC2164
cd prospectus_field_extraction/data
parallel -I[] curl "https://geco.amf-france.org/Bio/res_part.aspx?selectNRJ=OPCVM\&npos=[]" ::: $(seq 0 1 30) | pup '.ctcoltableresult2 tr json{}' | node -e "$PROCESS" >list_of_annotated_fund.json
cd ../..
