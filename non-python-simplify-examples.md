# JS Examples

## Example 1:

### Code Snippet:
```
const AppLoaderComponent = (props) => {
  const params = useParams();
  const appId = params.id;

  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => loadAppDetails(), []);

  const loadAppDetails = () => {
    appService.getApp(appId, 'edit').catch((error) => {
      handleError(error);
    });
  };

  const switchOrganization = (orgId) => {
    const path = `/apps/${appId}`;
    const sub_path = window?.public_config?.SUB_PATH ? stripTrailingSlash(window?.public_config?.SUB_PATH) : '';
    organizationService.switchOrganization(orgId).then(
      () => {
        window.location.href = `${sub_path}/${orgId}${path}`;
      },
      () => {
        return (window.location.href = `${sub_path}/login/${orgId}?redirectTo=${path}`);
      }
    );
  };

  const handleError = (error) => {
    try {
      if (error?.data) {
        const statusCode = error.data?.statusCode;
        if (statusCode === 403) {
          const errorObj = safelyParseJSON(error.data?.message);
          if (
            errorObj?.organizationId &&
            authenticationService.currentSessionValue.current_organization_id !== errorObj?.organizationId
          ) {
            switchOrganization(errorObj?.organizationId);
            return;
          }
          redirectToDashboard();
        } else if (statusCode === 401) {
          window.location = `${getSubpath() ?? ''}/login${
            !_.isEmpty(getWorkspaceId()) ? `/${getWorkspaceId()}` : ''
          }?redirectTo=${this.props.location.pathname}`;
          return;
        } else if (statusCode === 404 || statusCode === 422) {
          toast.error(error?.error ?? 'App not found');
        }
        redirectToDashboard();
      }
    } catch (err) {
      redirectToDashboard();
    }
  };

  return config.ENABLE_MULTIPLAYER_EDITING ? <RealtimeEditor {...props} /> : <Editor {...props} />;
};

export const AppLoader = withTranslation()(AppLoaderComponent);
```
### Result
```
Brief description of what is making the code complex currently.
The current code has a few areas that could be simplified:

The useEffect hook is using a function loadAppDetails that is defined after the hook. This can lead to confusion and potential bugs.
The switchOrganization function constructs a URL in a somewhat convoluted way.
The handleError function has a lot of nested conditionals and repeated code.
Improvement steps:

Move the loadAppDetails function definition above the useEffect hook.

Simplify the URL construction in the switchOrganization function.

Refactor the handleError function to reduce nested conditionals and repeated code.

Improved code:

const AppLoaderComponent = (props) => {
  const params = useParams();
  const appId = params.id;

  const loadAppDetails = () => {
    appService.getApp(appId, 'edit').catch(handleError);
  };

  useEffect(loadAppDetails, []);

  const switchOrganization = async (orgId) => {
    const path = `/apps/${appId}`;
    const sub_path = window?.public_config?.SUB_PATH ? stripTrailingSlash(window?.public_config?.SUB_PATH) : '';
    try {
      await organizationService.switchOrganization(orgId);
      window.location.href = `${sub_path}/${orgId}${path}`;
    } catch {
      window.location.href = `${sub_path}/login/${orgId}?redirectTo=${path}`;
    }
  };

  const handleError = (error) => {
    try {
      if (error?.data) {
        const statusCode = error.data?.statusCode;
        const errorObj = safelyParseJSON(error.data?.message);
        const orgId = errorObj?.organizationId;
        const currentOrgId = authenticationService.currentSessionValue.current_organization_id;

        if (statusCode === 403 && orgId && currentOrgId !== orgId) {
          switchOrganization(orgId);
          return;
        }

        if (statusCode === 401) {
          window.location = `${getSubpath() ?? ''}/login${
            !_.isEmpty(getWorkspaceId()) ? `/${getWorkspaceId()}` : ''
          }?redirectTo=${this.props.location.pathname}`;
          return;
        }

        if (statusCode === 404 || statusCode === 422) {
          toast.error(error?.error ?? 'App not found');
        }

        redirectToDashboard();
      }
    } catch (err) {
      redirectToDashboard();
    }
  };

  return config.ENABLE_MULTIPLAYER_EDITING ? <RealtimeEditor {...props} /> : <Editor {...props} />;
}
Brief description and explanation of the suggested improvement.
The loadAppDetails function is now defined before the useEffect hook, which makes the code easier to read and understand.
The switchOrganization function now uses async/await and a try/catch block to handle the promise, which simplifies the code and makes it easier to understand.
The handleError function has been refactored to reduce the amount of nested conditionals and repeated code. This makes the function easier to read and maintain.
```
