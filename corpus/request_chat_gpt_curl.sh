# POUR EXECUTER LE FICHIER : 'chemin du fichier'/request_chatgpt_curl.sh corpus.txt>output.txt
# corpus.txt est le fichier d'entrée contenant les requêtes à envoyer à ChatGPT.
# output.txt est le fichier du résultat, sous la forme "question": [réponse ChatGPT].
#!/bin/bash
echo "Question: extended response"
# Check if the file path is provided as an argument
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <file>"
  exit 1
fi

# Read file path from command line argument
file="$1"

# Check if the file exists
if [ ! -f "$file" ]; then
  echo "File not found: $file"
  exit 1
fi

while IFS= read -r line; do
  api_response=$(curl -s --max-time 30 https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer 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" \
  -d "{
     \"model\": \"gpt-3.5-turbo\",
     \"messages\": [
    {\"role\": \"user\", \"content\": \"$line ?\"}
     ],
     \"temperature\": 0.5,
     \"max_tokens\": 3000,
     \"n\": 1
  }")

  # Check if the API response is empty or null
  if [ -z "$api_response" ] || [ "$api_response" == "null" ]; then
    echo "API response is empty or null"
  else
    # Extract content from API response using jq
    content=$(echo "$api_response" | jq -r '.choices[].message.content')
    if [ -z "$content" ]; then
      echo "pas de reponse pour la question [ $line ]"
    else
      # Display the line and API response as $line: $content
      echo "\"$line\" : [$content]"
    fi
  fi
  sleep 30
done < "$file"
