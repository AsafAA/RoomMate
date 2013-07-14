#import "RMAPI.h"
#import "RMSettings.h"
#import "RMGroupID.h"
#import "RMUsername.h"

static NSString *kUpdateUserURLString = @"http://ec2-54-214-57-237.us-west-2.compute.amazonaws.com/add_user";
static NSString *kUpdateLocationURLString = @"http://ec2-54-214-57-237.us-west-2.compute.amazonaws.com/update_location";

@implementation RMAPI

+ (void)updateUser {
    RMSettings *settings = [RMSettings settings];

    if (settings.groupID != nil && settings.deviceToken != nil && settings.username != nil) {
        NSURL *url = [NSURL URLWithString:kUpdateUserURLString];
        NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:url];
        request.HTTPBody = [[NSString stringWithFormat:@"group_id=%@&phone_id=%@&phone_name=%@&dnd=%@", settings.groupID.string, settings.deviceToken, settings.username.string, (settings.privacyMode ? @"1" : @"0")] dataUsingEncoding:NSUTF8StringEncoding];
        request.HTTPMethod = @"POST";
        
        [NSURLConnection connectionWithRequest:request delegate:self];
    }
}

+ (void)updateLocation:(CLLocation *)location {
    RMSettings *settings = [RMSettings settings];

    if (settings.groupID != nil && settings.deviceToken != nil && settings.username != nil) {
        NSURL *url = [NSURL URLWithString:kUpdateLocationURLString];
        NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:url];
        request.HTTPBody = [[NSString stringWithFormat:@"group_id=%@&phone_id=%@&lat=%f&lon=%f&acc=%f", settings.groupID.string, settings.deviceToken, location.coordinate.latitude, location.coordinate.longitude, location.horizontalAccuracy] dataUsingEncoding:NSUTF8StringEncoding];
        request.HTTPMethod = @"POST";
        
        [NSURLConnection connectionWithRequest:request delegate:self];
    }
}

@end