import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class ApiService {
  static final ApiService _instance = ApiService._internal();
  factory ApiService() => _instance;
  final _storage = const FlutterSecureStorage();
  late Dio dio;
  String? _accesstoken;
  String? _refreshtoken;
  Function? onLogout;
  bool _isRefreshing = false;

  ApiService._internal() {
    dio = Dio(
      BaseOptions(
        baseUrl: "https://salemproject.pythonanywhere.com/api",
        connectTimeout: const Duration(seconds: 10),
        receiveTimeout: const Duration(seconds: 10),
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json",
        },
      ),
    );

    dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) {
       
          if (_accesstoken != null) {
            options.headers["Authorization"] = "Bearer $_accesstoken";
          }
          return handler.next(options);
        },
        onError: (error, handler) async {
          if (error.requestOptions.path == "/refresh/") {
            clearToken();
            await clearTokensFromStorage();
            if (onLogout != null) {
              onLogout!();
            }
            return handler.next(error);
          }
          if (error.response?.statusCode == 401) {
            if (_isRefreshing) {
              return handler.next(error);
            }
            _isRefreshing = true;
            final success = await refreshToken();
            _isRefreshing = false;

            if (success) {
              final requestOptions = error.requestOptions;

              requestOptions.headers["Authorization"] = "Bearer $_accesstoken";

              final response = await dio.fetch(requestOptions);

              return handler.resolve(response);
            } else {
              clearToken();
              await clearTokensFromStorage();
              if (onLogout != null) {
                onLogout!();
              }
            }
          }

          return handler.next(error);
        },
      ),
    );
  }

  Future<bool> refreshToken() async {

    if (_refreshtoken == null) return false;

    try {
      final refreshDio = Dio(
        BaseOptions(baseUrl: "https://salemproject.pythonanywhere.com/api/"),
      );

      final response = await refreshDio.post(
        "/refresh/",
        data: {"refresh": _refreshtoken},
      );
   

      final newAccess = response.data["access"];
      final newRefresh = response.data["refresh"];

      _accesstoken = newAccess;
      _refreshtoken = newRefresh;
      await saveTokens(newAccess, _refreshtoken!);

      return true;
    } catch (e) {
      return false;
    }
  }

  Future<void> saveTokens(String access, String refresh) async {
    await _storage.write(key: "access", value: access);
    await _storage.write(key: "refresh", value: refresh);
  }

  Future<void> loadTokens() async {
    _accesstoken = await _storage.read(key: "access");
    _refreshtoken = await _storage.read(key: "refresh");
  }

  Future<void> clearTokensFromStorage() async {
    await _storage.deleteAll();
  }

  void setAccessToken(String token) {
    _accesstoken = token;
  }

  void setRefreshToken(String token) {
    _refreshtoken = token;
  }

  void clearToken() {
    _accesstoken = null;
    _refreshtoken = null;
  }

  String? getAccessToken() => _accesstoken;
  String? getRefreshToken() => _refreshtoken;
}
