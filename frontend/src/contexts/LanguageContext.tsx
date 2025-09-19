import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { languages } from '@/services/api';

interface LanguageContextType {
  currentLanguage: string;
  changeLanguage: (langCode: string) => void;
  language: string;
  availableLanguages: typeof languages;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [currentLanguage, setCurrentLanguage] = useState(() => {
    // Get initial language from localStorage or default to 'en'
    return localStorage.getItem('nile-care-language') || 'en';
  });

  const changeLanguage = (langCode: string) => {
    setCurrentLanguage(langCode);
    localStorage.setItem('nile-care-language', langCode);
  };

  const language = languages.find(lang => lang.code === currentLanguage)?.name || 'English';

  useEffect(() => {
    // Ensure the language is persisted when the component mounts
    localStorage.setItem('nile-care-language', currentLanguage);
  }, [currentLanguage]);

  return (
    <LanguageContext.Provider
      value={{
        currentLanguage,
        changeLanguage,
        language,
        availableLanguages: languages
      }}
    >
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const context = useContext(LanguageContext);
  if (context === undefined) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
}