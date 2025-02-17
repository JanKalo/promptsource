import argparse
import textwrap

from promptsource.templates import TemplateCollection, INCLUDED_USERS
from promptsource.utils import get_dataset


parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument("dataset_path", type=str, help="path to dataset name")

args = parser.parse_args()
if "templates.yaml" not in args.dataset_path:
    exit()

path = args.dataset_path.split("/")

if path[2] in INCLUDED_USERS:
    dataset_name = f"{path[2]}/{path[3]}"
    subset_name = path[4] if len(path) == 6 else ""
else:
    dataset_name = path[2]
    subset_name = path[3] if len(path) == 5 else ""

template_collection = TemplateCollection()

dataset = get_dataset(dataset_name, subset_name)
splits = list(dataset.keys())

dataset_templates = template_collection.get_dataset(dataset_name, subset_name)
template_list = dataset_templates.all_template_names

width = 80
print("DATASET ", args.dataset_path)

# First show all the templates.
for template_name in template_list:
    template = dataset_templates[template_name]
    print("TEMPLATE")
    print("NAME:", template_name)
    print("Is Original Task: ", template.metadata.original_task)
    print(template.jinja)
    print()

# Show examples of the templates.
for template_name in template_list:
    template = dataset_templates[template_name]
    print()
    print("TEMPLATE")
    print("NAME:", template_name)
    print("REFERENCE:", template.reference)
    print("--------")
    print()
    print(template.jinja)
    print()

    for split_name in splits:
        dataset_split = dataset[split_name]

        print_counter = 0
        for example in dataset_split:
            print("\t--------")
            print("\tSplit ", split_name)
            print("\tExample ", example)
            print("\t--------")
            output = template.apply(example)
            if output == [""]:
                print("\t Blank result")
                continue

            xp, yp = output
            print()
            print("\tPrompt | X")
            for line in textwrap.wrap(xp, width=width, replace_whitespace=False):
                print("\t", line.replace("\n", "\n\t"))
            print()
            print("\tY")
            for i, y in enumerate(yp):
                if i > 0:
                    print()
                    print("\tY")
                for line in textwrap.wrap(y, width=width, replace_whitespace=False):
                    print("\t", line.replace("\n", "\n\t"))

            print_counter += 1
            if print_counter >= 10:
                break
