import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export const truncateText = (text: string, limit: number) => {
  if (text) {
    return text.length > limit ? `${text.slice(0, limit)}..` : text
  }
  return ''
}

export const isValidUrl = (url: string): boolean => {
  try {
    const pattern = new RegExp(
      '^https?:\\/\\/' +
        '((([a-zA-Z\\d]([a-zA-Z\\d-]*[a-zA-Z\\d])*)\\.)+[a-zA-Z]{2,}|' +
        'localhost|' +
        '\\d{1,3}(\\.\\d{1,3}){3})' +
        '(\\:\\d+)?' +
        '(\\/[-a-zA-Z\\d%@_.~+&:]*)*' +
        '(\\?[;&a-zA-Z\\d%@_.,~+&:=-]*)?' +
        '(\\#[-a-zA-Z\\d_]*)?$',
      'i'
    )

    return pattern.test(url.trim())
  } catch {
    return false
  }
}
