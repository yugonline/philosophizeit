import React, { useState, ChangeEvent, FormEvent } from 'react';
import axios from 'axios';
import './App.css';

type PromptType = 'dialectic' | 'hermeneutics';

interface ResponseData {
  response_text: string;
}

const App: React.FC = () => {
  const [promptType, setPromptType] = useState<PromptType>('dialectic');
  const [promptText, setPromptText] = useState<string>('');
  const [response, setResponse] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isSubmitted, setIsSubmitted] = useState<boolean>(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>): Promise<void> => {
    event.preventDefault();
    setIsLoading(true);
    setIsSubmitted(true);

    try {
      const result = await axios.post<ResponseData>('/generate-response', { prompt_type: promptType, text: promptText });
      setResponse(result.data.response_text);
    } catch (error) {
      console.error(error);
    }

    setIsLoading(false);
  };

  return (
      <div className="App">
        <h1>Philosopher Says</h1>
        <form onSubmit={handleSubmit}>
          <label htmlFor="promptType">Choose a prompt type:</label>
          <select
              id="promptType"
              value={promptType}
              onChange={(event: ChangeEvent<HTMLSelectElement>) => setPromptType(event.target.value as PromptType)}
          >
            <option value="dialectic">Dialectic</option>
            <option value="hermeneutics">Hermeneutics</option>
          </select>

          <label htmlFor="promptText">Enter a prompt:</label>
          <textarea
              id="promptText"
              value={promptText}
              onChange={(event: ChangeEvent<HTMLTextAreaElement>) => setPromptText(event.target.value)}
              disabled={isLoading}
          />

          <button type="submit" disabled={isLoading}>
            Submit
          </button>

          {isLoading && (
              <div className="loading">
                <div className="spinner" />
              </div>
          )}
        </form>

        {isSubmitted && !isLoading && (
            <div className="response">
              <h2>Your Input:</h2>
              <p>{promptText}</p>

              <h2>Philosopher Will Say:</h2>
              <p>{response}</p>
            </div>
        )}
      </div>
  );
};

export default App;
