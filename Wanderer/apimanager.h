#ifndef APIMANAGER_H
#define APIMANAGER_H

#include <QObject>
#include <QNetworkAccessManager>

class ApiManager : public QObject
{
    Q_OBJECT

public:
    explicit ApiManager(QObject *parent = nullptr);
    ~ApiManager();
public slots:
   Q_INVOKABLE void loginUser(const QString& login, const QString& password);
   Q_INVOKABLE void registerUser(const QString &login, const QString &password, const QString& passwordRepeated, const QString& emailAddress);
   Q_INVOKABLE void logoutUser();
   Q_INVOKABLE void forgotPassword(const QString& emailAddress);
   Q_INVOKABLE void forgotPasswordCheckToken(const QString& emailAddress, const QString& code);
   Q_INVOKABLE void forgotPasswordConfirm(const QString& emailAddress, const QString& code, const QString &password, const QString& passwordRepeated);

signals:
   void loginCorrect(const QString& token);
   void loginFailed(const QString& errorMessage);
   void registerCorrect();
   void registerFailed(const QString& errorMessage);
   void logoutCorrect();
   void logoutFailed(const QString& errorMessage);
   void forgotPasswordCorrect();
   void forgotPasswordFailed(const QString& errorMessage);
   void forgotPasswordCheckTokenCorrect();
   void forgotPasswordCheckTokenFailed(const QString& errorMessage);
   void forgotPasswordConfirmCorrect();
   void forgotPasswordConfirmFailed(const QString& errorMessage);

private:
    QNetworkAccessManager* networkManager;
    QString m_token;

    QByteArray prepareLoginData(const QString &login, const QString &password);
    QByteArray prepareRegisterData(const QString &login, const QString &password, const QString& passwordRepeated, const QString& emailAddress);
    QByteArray prepareForgotPasswordData(const QString& emailAddress);
    QByteArray prepareForgotPasswordCheckToken(const QString& emailAddress, const QString& code);
    QByteArray prepareForgotPasswordConfirm(const QString& emailAddress, const QString& code, const QString &password, const QString& passwordRepeated);

    void handleLoginResponse(QNetworkReply *reply);
    void handleRegisterResponse(QNetworkReply *reply);
    void handleLogoutResponse(QNetworkReply *reply);
    void handleForgotPasswordResponse(QNetworkReply *reply);
    void handleForgotPasswordCheckToken(QNetworkReply *reply);
    void handleForgotPasswordConfirm(QNetworkReply *reply);

    QJsonObject parseResponseToJson(QNetworkReply* reply);
    std::vector<QString> parseErrorResponse(const QJsonObject& apiJsonResponse);
    QString getErrorResponseInString(const QJsonObject& apiJsonResponse);
    QString getErrorMessages(const std::vector<QString>& errors);
};


#endif // APIMANAGER_H
