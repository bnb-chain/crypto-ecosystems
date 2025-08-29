<h3 align="center">
<img width="300" alt="crypto_ecosystems" src="https://github.com/user-attachments/assets/3e0c7ee0-67c3-44a3-a575-6a1cb1824788" />
</h3>

Crypto Ecosystems is a taxonomy of open source blockchain, web3, cryptocurrency, and decentralized ecosystems and their code repositories.  This dataset is not complete, and hopefully it never will be as there are new ecosystems and repositories created every day.

## How to use this taxonomy
The taxonomy can be used to generate the set of crypto ecosystems, their corresponding sub ecosystems, and repositories at a particular time.
### 🖼️ GUI Mode
You can use the taxonomy viewer at [crypto-ecosystems.xyz](https://crypto-ecosystems.xyz).  Here you can query for ecosystems and repos as well as export all of the repos for specific ecosystems.
<div align="center">
<img width="800" alt="image" src="https://github.com/user-attachments/assets/8003fa92-6874-42d8-a398-7b1741964498" />
</div>

### 💻 CLI Mode
For more data science uses, one can export the taxonomy to a json format by using the following command:
```bash
./run.sh export exports.jsonl
```

If you want to export a single ecosystem, its sub ecosystems, and its repositories, you can use the `-e` parameter to specify a particular ecosystem.
```bash
./run.sh export -e Bitcoin bitcoin.jsonl
```

The export format is one json entry per line like the following:
```json
{"eco_name":"Bitcoin","branch":["Lightning"],"repo_url":"https://github.com/alexbosworth/balanceofsatoshis","tags":["#developer-tool"]}
{"eco_name":"Bitcoin","branch":["Lightning"],"repo_url":"https://github.com/bottlepay/lnd","tags":[]}
```
By using the branch attribute, you can see how particular repos are attributed to the parent ecosystem.

## How to update the taxonomy
There is a domain specific language (DSL) containing the keywords that can make changes to the taxonomy.  You specify migrations by using files of the format
```bash
migrations/YYYY-MM-DDThhmmss_description_of_your_migration
```

The datetime format is a loosely ISO8601 but without the ':' characters to make them valid files on Windows.

Some examples migration filenames could be:
```bash
migrations/2009-01-03T181500_add_bitcoin
migrations/2015-07-30T152613_add_ethereum
```

Simply create your new migration and add changes to the taxonomy using the keywords discussed below.

## Data Format

### Example: Adding an ecosystem and connecting it.
```lua
-- Add ecosystems with the ecoadd keyword.  You can start a line with -- to denote a comment.
ecoadd Lightning
-- Add repos to ecosystems using the repadd keyword
repadd Lightning https://github.com/lightningnetwork/lnd #protocol
-- Connect ecosystems using the ecocon keyword.
-- The following connects Lighting as a sub ecosystem of Bitcoin.
ecocon Bitcoin Lighting
```
  
## How to Give Attribution For Usage of the Electric Capital Crypto Ecosystems

The repository is licensed under [MIT license with attribution](https://github.com/electric-capital/crypto-ecosystems/blob/master/LICENSE).

To use the Electric Capital Crypto Ecosystems Map in your project, you will need an attribution.

Attribution needs to have 3 components:

1. Source: “Electric Capital Crypto Ecosystems”
2. Link: https://github.com/electric-capital/crypto-ecosystems
3. Logo: [Link to logo](static/electric_capital_logo_transparent.png)

Optional:
Everyone in the crypto ecosystem benefits from additions to this repository.
It is a help to everyone to include an ask to contribute next to your attribution.

Sample request language: "If you’re working in open source crypto, submit your repository here to be counted."

<ins>Sample attribution</ins>

Data Source: [Electric Capital Crypto Ecosystems](https://github.com/electric-capital/crypto-ecosystems)

If you’re working in open source crypto, submit your repository [here](https://github.com/electric-capital/crypto-ecosystems) to be counted.

Thank you for contributing and for reading the contribution guide! ❤️

# CSV to Migration Converter

This script converts the `sheet2.csv` file into a migration file with the format:

```
repadd "BNB Chain" https://github.com/fstswap/fstswap.github.io #FstSwap
repadd "BNB Chain" https://github.com/Entangle-Protocol/corechain #Entangle
repadd "BNB Chain" https://github.com/dawar2151/x-wallet-bulksender-smart-contracts #Token-Bulk-Sender
```

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## Usage

1. Make sure `sheet2.csv` is in the same directory as the script
2. Run the script:

```bash
# On Windows:
python csv_to_migration.py

# On macOS/Linux:
python3 csv_to_migration.py
```

3. The script will generate a `migration_output.txt` file with the converted format

## What the script does

- Reads the CSV file and extracts the `github_link` and `Name` columns
- Formats each row into the migration format: `repadd "BNB Chain" {github_link} #{cleaned_project_name}`
- Cleans project names by replacing spaces with hyphens and removing special characters
- Skips rows with missing data
- Shows a preview of the first 10 lines of output

## Output

The script will create a file called `migration_output.txt` that you can then copy into your migration file.

## Example output

```
repadd "BNB Chain" https://github.com/ultiverse-io/ #Ultiverse
repadd "BNB Chain" https://github.com/Orbofi #Orbofi
repadd "BNB Chain" https://github.com/Orbofi #Orbofi
repadd "BNB Chain" https://github.com/HODL-org #HODL
repadd "BNB Chain" https://github.com/Aegis-im #Aegis
```

## Troubleshooting

- Make sure `sheet2.csv` exists in the same directory
- Ensure you have Python 3.6+ installed
- Check that the CSV file has the expected column names: `Name` and `github_link`