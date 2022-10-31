import pickle

import numpy as np
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, Dataset


class TaskDataset(Dataset):
    def __init__(self, X, Y, transforms=None):
        self.X = X
        self.Y = Y
        self.transforms = transforms

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        image = np.load(self.X[idx]).astype(np.float32)
        label = self.Y[idx]
        if self.transforms is not None:
            image = self.transforms(image)
        elif self.transforms is None:
            image = transforms.ToTensor()(image)
        return image, label


def main():
    with open("task/diagnosis_CD8_healthy_timepoint1_CD8.pkl", "rb") as f:
        task = pickle.load(f)

    train_transform = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.RandomRotation(20),
            transforms.RandomHorizontalFlip(),
            transforms.RandomVerticalFlip(),
        ]
    )

    test_transform = transforms.Compose([transforms.ToTensor()])

    train_dataset = TaskDataset(
        task["train_X"], task["train_Y"], transforms=train_transform
    )
    train_dataloader = DataLoader(train_dataset, batch_size=4, shuffle=True)
    for i, (images, labels) in enumerate(train_dataloader):
        print(images.shape, labels.shape)
        break


if __name__ == "__main__":
    main()
