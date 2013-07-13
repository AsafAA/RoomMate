#import "RMAPI.h"
#import "RMSettings.h"
#import "RMGroupID.h"
#import "RMUsername.h"

static NSString *kUpdateUserURLString = @"http://localhost/add_user";
static NSString *kUpdateLocationURLString = @"http://localhost/update_location";

@implementation RMAPI

+ (void)updateUser {
    NSURL *url = [NSURL URLWithString:kUpdateUserURLString];
    NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:url];
    
    RMSettings *settings = [RMSettings settings];
    NSDictionary *dict = @{@"group_id": settings.groupID.string,
                           @"phone_id": @"DEVICE TOKEN",
                           @"phone_name": settings.username.string,
                           @"dnd": (settings.privacyMode ? @1 : @0)};
    NSData *json = [NSJSONSerialization dataWithJSONObject:dict options:0 error:nil];
    request.HTTPBody = json;
    
    [NSURLConnection connectionWithRequest:request delegate:nil];
}

+ (void)updateLocation:(CLLocation *)location {
    NSURL *url = [NSURL URLWithString:kUpdateLocationURLString];
    NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:url];
    
    RMSettings *settings = [RMSettings settings];
    NSDictionary *dict = @{@"group_id": settings.groupID.string,
                           @"phone_id": @"DEVICE TOKEN",
                           @"lat": [NSNumber numberWithDouble:location.coordinate.latitude],
                           @"lon": [NSNumber numberWithDouble:location.coordinate.longitude],
                           @"acc": [NSNumber numberWithDouble:location.horizontalAccuracy]};
    NSData *json = [NSJSONSerialization dataWithJSONObject:dict options:0 error:nil];
    request.HTTPBody = json;
    
    [NSURLConnection connectionWithRequest:request delegate:nil];
}

@end