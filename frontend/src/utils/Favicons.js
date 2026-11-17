export function getFavicon(year) {

  if (year >= 1965) {
    return "/Maple_Leaf.svg";
  }

  else if (year >= 1957) {
    return "/Arms_of_Canada_1957.svg";
  }

  else if (year >= 1921) {
    return "/Arms_of_Canada_1921.svg";
  }

  return "/Royal_Union_Flag.svg";
}