#import "RMSettingsViewController.h"
#import "RMSettings.h"
#import "RMMessager.h"
#import "RMGroupID.h"
#import "RMUsername.h"

@implementation RMSettingsViewController

- (IBAction)done:(id)sender {
    RMSettings *settings = [RMSettings settings];
    [settings save];

    [self dismissViewControllerAnimated:YES completion:nil];
}

- (IBAction)dismissKeyboard:(id)sender {
    [sender resignFirstResponder];
    [self saveName];
}

- (void)viewWillAppear:(BOOL)animated {
    RMSettings *settings = [RMSettings settings];
    self.nameField.text = settings.username.string;
}

- (void)viewWillDisappear:(BOOL)animated {
    [self saveName];
}

- (void)saveName {
    RMSettings *settings = [RMSettings settings];
    NSString *name = self.nameField.text;
    
    if ([name isEqualToString:@""]) {
        self.nameField.text = settings.username.string;
    } else {
        settings.username = [[RMUsername alloc] initWithString:name];
    }
}

- (void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath {
    [tableView deselectRowAtIndexPath:indexPath animated:YES];
    
    if (indexPath.section == 1) {
        if (indexPath.row == 0) {
            RMMessager *messager = [RMMessager messager];
            [messager showOnParent:self];
        } else {
            RMSettings *settings = [RMSettings settings];
            settings.groupID = [[RMGroupID alloc] init];
            [settings save];
            
            RMMessager *messager = [RMMessager messager];
            [messager showOnParent:self];
        }
    }
}

@end