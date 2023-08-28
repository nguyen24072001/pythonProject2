import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
import torchvision.datasets as datasets
from torch.utils.data import DataLoader


# Define the neural network architecture


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1)
        self.conv4 = nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1)
        self.fc1 = nn.Linear(128 * 8 * 8, 512)
        self.fc2 = nn.Linear(512, 128)

    def forward(self, x):
        x = nn.functional.relu(self.conv1(x))
        x = nn.functional.relu(self.conv2(x))
        x = nn.functional.max_pool2d(x, 2)
        x = nn.functional.relu(self.conv3(x))
        x = nn.functional.relu(self.conv4(x))
        x = nn.functional.max_pool2d(x, 2)
        x = x.view(-1, 128 * 8 * 8)
        x = nn.functional.relu(self.fc1(x))
        x = self.fc2(x)
        return x


# Define the triplet loss function
class TripletLoss(nn.Module):
    def __init__(self, margin=1.0):
        super(TripletLoss, self).__init__()
        self.margin = margin

    def forward(self, anchor, positive, negative):
        distance_positive = (anchor - positive).pow(2).sum(1)
        distance_negative = (anchor - negative).pow(2).sum(1)
        loss = nn.functional.relu(distance_positive - distance_negative + self.margin)
        return loss.mean()


# Define the training loop
def train(model, train_loader, optimizer, criterion, device):
    model.train()
    running_loss = 0.0
    for i, (anchor, positive, negative) in enumerate(train_loader):
        anchor, positive, negative = anchor.to(device), positive.to(device), negative.to(device)
        optimizer.zero_grad()
        output_anchor, output_positive, output_negative = model(anchor), model(positive), model(negative)
        loss = criterion(output_anchor, output_positive, output_negative)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    return running_loss / len(train_loader)


# Define the main function
def main():
    # Set up the hyperparameters
    batch_size = 64
    learning_rate = 0.001
    num_epochs = 10
    margin = 1.0

    # Set up the device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # Load the CIFAR-10 dataset
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
    train_dataset = datasets.CIFAR10(root='./data', train=True, download=True, transform=transform)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    # Set up the model, optimizer, and loss function
    model = Net().to(device)
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    criterion = TripletLoss(margin=margin)

    # Train the model
    for epoch in range(num_epochs):
        loss = train(model, train_loader, optimizer, criterion, device)
        print('Epoch [{}/{}], Loss: {:.4f}'.format(epoch + 1, num_epochs, loss))

    # Save the model
    torch.save(model.state_dict(), 'model.pth')


if __name__ == '__main__':
    main()
