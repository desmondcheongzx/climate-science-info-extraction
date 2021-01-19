import csv
from spacy.lang.en import English

nlp = English()
tokenizer = nlp.Defaults.create_tokenizer(nlp)


class DataItem():
    def __init__(self, title, abstract):
        self.tokens = []
        self.labels = []
        doc = tokenizer(abstract)
        self.tokens.append('*START-SENTENCE*')
        self.labels.append(title)
        for i, token in enumerate(doc):
            self.tokens.append(token)
            self.labels.append('O')
            if token.text == '.':
                self.tokens.append('*END-SENTENCE*')
                self.labels.append(title)
                if i < len(doc) - 1:
                    self.tokens.append('*START-SENTENCE*')
                    self.labels.append(title)
        pass

    def get_rows(self):
        rows = []
        for token, label in zip(self.tokens, self.labels):
            rows.append((token, label))
        return rows

    def __repr__(self):
        output_str = ''
        for token, label in self.get_rows():
            output_str += f'{token}, {label}\n'
        return output_str


def write_data(source_file, destination_file):
    with open(destination_file, 'w+') as csvfile:
        writer = csv.writer(csvfile)

        title = None
        abstract = None
        with open(source_file, 'r') as abstracts_file:
            for line in abstracts_file:
                line = line.rstrip()
                if '---' in line:
                    title = None
                    abstract = None
                    continue
                if title is None:
                    title = line
                    continue
                abstract = line
                data_item = DataItem(title, abstract)
                for row in data_item.get_rows():
                    writer.writerow(row)


if __name__ == "__main__":
    write_data('data/to_label_abstracts.txt', 'data/papers/labeled_dev.csv')
    write_data('data/unlabeled_abstracts.txt', 'data/papers/unlabeled.csv')
